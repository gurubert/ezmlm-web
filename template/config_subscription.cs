<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ConfigSub) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ConfigSub) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.ConfigSub) ?> </legend>

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="config_subset" value="subscription" />

		<ul>

			<!-- public subsccription and archive -->
			<li><?cs call:checkbox("p") ?></li>

			<!-- do not require confirmation for subscription -->
			<li><?cs call:checkbox("h") ?></li>

			<!-- do not require confirmation for unsubscribe -->
			<li><?cs call:checkbox("j") ?></li>

			<!-- moderate subscription -->
			<li><?cs call:checkbox("s") ?>
				<ul>
				<!-- custom path to subscription moderators -->
				<li><?cs call:setting("8") ?></li>
				</ul></li>

			<li><!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

			<input type="hidden" name="action" value="config_do" />
			<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button></li>
		</ul>

	</form>

</fieldset>
