<div class="title">
	<h1><?cs var:Lang.Title.ConfigAdmin ?></h1>
</div>

<div class="introduction">
	<p><?cs var:Lang.Introduction.ConfigAdmin ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:Lang.Legend.ConfigAdmin ?></legend>

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="config_subset" value="admin" />

		<ul>

			<li><?cs call:checkbox("r") ?></li>
			<li><?cs call:checkbox("l") ?></li>
			<li><?cs call:checkbox("n") ?></li>
			<li><?cs call:setting("8") ?></li>
		
			<!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

		<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
		</ul>

	</form>
</fieldset>

