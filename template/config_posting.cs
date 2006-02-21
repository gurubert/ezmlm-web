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

			<!-- message size limit -->
			<li><input type="checkbox" name="msgsize_max_state"
				value="selected" id="msgsize_max_state" <?cs
				if:Data.List.MsgSize.Max>0 ?>checked="checked"<?cs /if ?> />
				<label for="msgsize_max_state"><?cs var:html_escape(Lang.Misc.MessageSize.Max) ?></label>
				<ul><li><input type="text" name="msgsize_max_value" size="10"
				style="text-align:right" value="<?cs
				alt:Data.List.MsgSize.Max ?>30000<?cs /alt ?>" /> <?cs
				var:html_escape(Lang.Misc.MessageSize.Unit) ?></li></ul></li>
			<li><input type="checkbox" name="msgsize_min_state"
				value="selected" id="msgsize_min_state" <?cs
				if:Data.List.MsgSize.Min>0 ?>checked="checked"<?cs /if ?> />
				<label for="msgsize_min_state"><?cs var:html_escape(Lang.Misc.MessageSize.Min) ?></label>
				<ul><li><input type="text" name="msgsize_min_value" size="10"
				style="text-align:right" value="<?cs
				alt:Data.List.MsgSize.Min ?>2<?cs /alt ?>" /> <?cs
				var:html_escape(Lang.Misc.MessageSize.Unit) ?></li></ul></li>

			<!-- mimeremove and mimereject -->
			<li><?cs call:checkbox("x") ?>
				<?cs if:(Data.List.Options.x == 1) ?><ul>
				<!-- turn off mimeremove, if "-x" is not activated, as it will be
						removed during the next config_update -->
					<li><?cs var:html_escape(Lang.Misc.MimeReject) ?>:<br/>
						<textarea name="mimereject" rows="4" cols="70"><?cs
						var:html_escape(Data.List.MimeReject) ?></textarea></li>
				</ul></li><?cs /if ?>

			<li><!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

			<input type="hidden" name="action" value="config_do" />
			<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button></li>
		</ul>

	</form>

</fieldset>
