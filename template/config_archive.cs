<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ConfigArchive) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ConfigArchive) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.ConfigArchive) ?> </legend>

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="config_subset" value="archive" />

		<ul>
		
			<li><?cs call:checkbox("a") ?></li>
			<li><?cs call:checkbox("p") ?></li>
			<li><?cs call:checkbox("b") ?></li>
			<li><?cs call:checkbox("g") ?></li>
			<li><?cs call:checkbox("i") ?></li>
		
			<li><!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

			<input type="hidden" name="action" value="config_do" />
			<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button></li>
		</ul>

	</form>
</fieldset>

