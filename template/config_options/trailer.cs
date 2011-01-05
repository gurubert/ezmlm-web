<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<!-- trailing text -->
<?cs call:checkbox("t") ?>
	<?cs if:(Data.List.Options.t == 1) ?>
	<!-- turn off trailer, if "-t" is not activated, as it will be
		removed during the next config_update -->
	<ul><pre style="background: #eed;"><?cs var:html_escape(Data.List.TrailingText) ?></pre></ul><?cs /if ?>
