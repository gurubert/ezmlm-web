<?cs if:Data.List.Features.GpgKeyRing ?>
<!-- comment for the key (second part of the human readable key description) -->

<label for="gnupg_keycomment"><?cs var:html_escape(Lang.Misc.GnupgKeyComment) ?>:</label>
	<input type="text" name="gnupg_keycomment" id="gnupg_keycomment" size="25"
		value="Mailing list" />
<?cs /if ?>

