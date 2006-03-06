<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ListCreate) ?></h1>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.ListCreate) ?> </legend>

	<form method="post" action="<?cs call:link("","","","","","") ?>" enctype="application/x-www-form-urlencoded">
		
		<?cs call:show_options(UI.Options.Create) ?>

		<!-- include default form values -->
		<?cs include:TemplateDir + '/form_common.cs' ?>

		<input type="hidden" name="action" value="list_create_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.Create) ?></button>
	</form>

</fieldset>
