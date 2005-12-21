<div class="title">
	<h1><?cs var:Lang.Title.ConfigPosting ?></h1>
</div>

<div class="introduction">
	<p><?cs var:Lang.Introduction.ConfigPosting ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:Lang.Legend.ConfigPosting ?></legend>

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

			<!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

		<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
		</ul>

	</form>

</fieldset>
