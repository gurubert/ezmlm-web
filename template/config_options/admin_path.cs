<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<?cs if:Data.List.Options.r ?>
	<!-- custom path to remote administrators -->
	<?cs call:setting("9") ?><?cs
		if:((Data.List.Settings.8.state == 1) && (Data.List.Settings.9.state == 1))
			?>(<?cs var:Lang.Misc.ModSubOverridesRemote ?>)<?cs /if ?>
<?cs /if ?>
