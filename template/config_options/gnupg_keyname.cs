<?cs if:Data.List.Features.Crypto ?>
<!-- name of the key (first part of the human readable key description) -->

<label for="gnupg_keyname"><?cs var:html_escape(Lang.Misc.GnupgKeyName) ?>:</label>
	<input type="text" name="gnupg_keyname" id="gnupg_keyname" size="25"
		value="<?cs var:html_escape(Data.List.Name) ?>" />
<?cs /if ?>

