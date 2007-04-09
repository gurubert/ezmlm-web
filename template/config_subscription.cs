<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ConfigSub) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ConfigSub) ?></p>
</div>

<fieldset>
	<legend><?cs var:html_escape(Lang.Legend.ConfigSub) ?> </legend>

	<?cs call:form_header("config_subscription", "") ?>
		<input type="hidden" name="config_subset" value="subscription" />

		<?cs call:show_options(UI.Options.Config.Subscription) ?>

		<input type="hidden" name="action" value="config_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button>

	</form>

</fieldset>
