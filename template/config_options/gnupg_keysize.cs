<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<!-- length of the key (bytes) -->
<select name="setting_gnupg_keysize" size="1" id="setting_gnupg_keysize">
	<option>1024</option>
	<option selected="selected">2048</option>
	<option>4096</option>
</select>
<label for="setting_gnupg_keysize"><?cs var:Lang.Misc.GnupgKeySize ?></label>

