<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<!-- ezmlm-web administators -->
<?cs var:html_escape(Lang.Misc.AllowedToEdit) ?> 
	<ul><li><input type="text"
	name="webusers" value="<?cs var:html_escape(Data.List.WebUsers)
	?>" size="40" /><br/>
	</li></ul>
