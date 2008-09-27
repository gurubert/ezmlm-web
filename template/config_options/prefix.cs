<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<!-- subject prefix -->
<?cs call:checkbox("f") ?>
	<ul><li><input type="text" name="prefix" value="<?cs
		var:html_escape(Data.List.Prefix) ?>" size="60" />
	</li></ul>
