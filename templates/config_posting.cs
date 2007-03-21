<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ConfigPosting) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ConfigPosting) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.ConfigPosting) ?> </legend>

	<form method="post" action="<?cs call:link("","","","","","") ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="config_subset" value="posting" />

		<?cs call:show_options(UI.Options.Config.Posting) ?>

		<!-- include default form values -->
		<?cs include:TemplateDir + '/form_common.cs' ?>

		<input type="hidden" name="action" value="config_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button>

	</form>

</fieldset>
