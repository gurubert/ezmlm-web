<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ConfigPosting) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ConfigPosting) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.ConfigPosting) ?> </legend>

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="config_subset" value="posting" />

		<ul>

			<!-- use deny list -->
			<li><?cs call:checkbox("k") ?></li>

			<!-- only subscribers may post -->
			<li><?cs call:checkbox("u") ?></li>

			<!-- require confirmation from poster -->
			<li><?cs call:checkbox("y") ?></li>

			<!-- posted messages are moderated -->
			<li><?cs call:checkbox("m") ?>
				<ul>
					<!-- only moderators may post -->
					<li><?cs call:checkbox("o") ?></li>

					<!-- nesage moderator -->
					<li><?cs call:setting("7") ?></li>
				</ul></li>

			<li><!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

		<input type="hidden" name="action" value="config_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button></li>
		</ul>

	</form>

</fieldset>
