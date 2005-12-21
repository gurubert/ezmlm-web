<div class="title">
	<h1><?cs var:Lang.Title.ConfigArchive ?></h1>
</div>

<div class="introduction">
	<p><?cs var:Lang.Introduction.ConfigArchive ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:Lang.Legend.ConfigArchive ?></legend>

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="config_subset" value="archive" />

		<ul>
		
			<li><?cs call:checkbox("a") ?></li>
			<li><?cs call:checkbox("p") ?></li>
			<li><?cs call:checkbox("b") ?></li>
			<li><?cs call:checkbox("g") ?></li>
			<li><?cs call:checkbox("i") ?></li>
		
			<!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

			<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
		</ul>

	</form>
</fieldset>

