<!-- turn off mimermove, if "-x" is not activated, as it will be
	removed during the next config_update -->
<?cs var:html_escape(Lang.Misc.MimeRemove) ?>:<br/>
	<textarea name="mimeremove" rows="4" cols="70"><?cs
	var:html_escape(Data.List.MimeRemove) ?></textarea>
