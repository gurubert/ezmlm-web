<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ConfigProcess) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ConfigProcess) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.ConfigProcess) ?> </legend>

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="config_subset" value="processing" />

		<ul>

			<!-- subject prefix -->
			<li><?cs call:checkbox("f") ?>
				<ul><li><input type="text" name="prefix" value="<?cs
					var:html_escape(Data.List.Prefix) ?>" size="70" />
				</li></ul></li>

			<!-- trailing text -->
			<li><?cs call:checkbox("t") ?>
				<?cs if:(Data.List.Options.t == 1) ?>
				<!-- turn off mimeremove, if "-x" is not activated, as it will be
					removed during the next config_update -->
					<ul><li><textarea name="trailing_text" rows="3" cols="72"><?cs
						var:html_escape(Data.List.TrailingText) ?></textarea></li>
					</ul></li><?cs /if ?>

			<!-- from address -->
			<li><?cs call:setting("3") ?></li>

			<!-- mimeremove and mimereject -->
			<li><?cs call:checkbox("x") ?>
				<?cs if:(Data.List.Options.x == 1) ?><ul>
				<!-- turn off mimeremove, if "-x" is not activated, as it will be
						removed during the next config_update -->
					<li><?cs var:html_escape(Lang.Misc.MimeRemove) ?>:<br/>
						<textarea name="mimeremove" rows="4" cols="70"><?cs
						var:html_escape(Data.List.MimeRemove) ?></textarea></li>
				</ul></li><?cs /if ?>

			<!-- headerremove -->
			<li><?cs var:html_escape(Lang.Misc.HeaderRemove) ?>:<br/>
				<ul><li><textarea name="headerremove" rows="5" cols="70"><?cs
				var:html_escape(Data.List.HeaderRemove) ?></textarea></li></ul></li>

			<!-- headeradd -->
			<li><?cs var:html_escape(Lang.Misc.HeaderAdd) ?>:<br/>
				<ul><li><textarea name="headeradd" rows="5" cols="70"><?cs
				var:html_escape(Data.List.HeaderAdd) ?></textarea></li></ul></li>

			<li><!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

			<input type="hidden" name="action" value="config_do" />
			<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button></li>

		</ul>
	</form>
</fieldset>

<?cs include:TemplateDir + '/help_tag_susbtitution.cs' ?>
