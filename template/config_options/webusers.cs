<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<!-- ezmlm-web administators -->
<?cs var:html_escape(Lang.Misc.AllowedToEdit) ?> 
	<ul><li><input type="text"
	name="webusers" value="<?cs if:Data.List.WebUsers
			?><?cs var:html_escape(Data.List.WebUsers) ?><?cs
		else ?><?cs
			var:html_escape(Data.WebUser.UserName)
	?><?cs /if ?>" size="40" /><br/>
	</li></ul>
