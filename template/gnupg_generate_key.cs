<div class="title">
	<h1><?cs var:html_escape(Lang.Title.GnupgGenerateKey) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.GnupgGenerateKey) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.GnupgGenerateKey) ?> </legend>

	<form method="post" action="<?cs call:link("","","","","","") ?>" enctype="application/x-www-form-urlencoded">

		<input type="hidden" name="gnupg_subset" value="generate_key" />
		
		<?cs call:show_options(UI.Options.GenerateKey) ?>

		<!-- include default form values -->
		<?cs include:TemplateDir + '/form_common.cs' ?>

		<input type="hidden" name="action" value="gnupg_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.GnupgGenerateKey) ?></button>
	</form>

</fieldset>

