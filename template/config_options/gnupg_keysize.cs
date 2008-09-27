<?cs if:Data.List.Features.GpgKeyRing ?>
<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<!-- length of the key (bytes) -->
<label for="gnupg_keysize"><?cs var:html_escape(Lang.Misc.GnupgKeySize) ?>:</label>
<select name="gnupg_keysize" size="1" id="gnupg_keysize">
	<option>1024</option>
	<option selected="selected">2048</option>
	<option>4096</option>
</select>
<?cs /if ?>

