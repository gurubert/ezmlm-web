<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<!-- charset -->
<?cs if:Data.List.CharSet ?>
	<label for="list_charset"><?cs var:html_escape(Lang.Misc.ListCharset)
			?>:</label>
		<input type="text" name="list_charset" id="list_charset" size="30"
			value="<?cs var:Data.List.CharSet ?>" /><?cs /if ?>
