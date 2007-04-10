<div class="title">
	<h1><?cs var:html_escape(Lang.Title.GnupgGenerateKey) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.GnupgGenerateKey) ?></p>
</div>

<fieldset>
	<legend><?cs var:html_escape(Lang.Legend.GnupgGenerateKey) ?> </legend>

	<?cs call:form_header("gnupg_generate_key") ?>

		<input type="hidden" name="gnupg_subset" value="generate_key" />
		
		<?cs call:show_options(UI.Options.GenerateKey) ?>

	<ul><li>
		<input type="hidden" name="action" value="gnupg_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.GnupgGenerateKey) ?></button></li></ul>
	</form>

</fieldset>

