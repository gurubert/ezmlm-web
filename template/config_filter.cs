<div class="title">
	<h1><?cs var:Lang.Title.ConfigFilter ?></h1>
</div>

<div class="introduction">
	<p><?cs var:Lang.Introduction.ConfigFilter ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:Lang.Legend.ConfigFilter ?></legend>

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="config_subset" value="filter" />

		<ul>

			<!-- subject prefix -->
			<li><?cs call:checkbox("f") ?>
				<ul><li><input type="text" name="prefix" value="<?cs
					var:Data.List.Prefix ?>" <?cs call:help_title("Prefix")
					?> size="70" />
				</li></ul></li>

			<!-- trailing text -->
			<li><?cs call:checkbox("t") ?>
				<?cs if:(Data.List.Options.t == 1) ?><ul>
				<!-- turn off mimermove, if "-x" is not activated, as it will be
					removed during the next config_update -->
					<ul><li><textarea name="trailing_text" rows="3" cols="72"><?cs
						var:html_escape(Data.List.TrailingText) ?></textarea></li>
					</ul></li><?cs /if ?>

			<!-- from address -->
			<li><?cs call:setting("3") ?></li>

			<!-- mimeremove -->
			<li><?cs call:checkbox("x") ?>
				<?cs if:(Data.List.Options.x == 1) ?><ul>
				<!-- turn off mimermove, if "-x" is not activated, as it will be
						removed during the next config_update -->
					<li><?cs var:Lang.Misc.MimeRemove ?>:<br/>
						<textarea name="mimeremove" rows="5" cols="70"><?cs
						var:html_escape(Data.List.MimeRemove) ?></textarea></li>
				</ul></li><?cs /if ?>

			<!-- message size limit -->
			<li><input type="checkbox" name="msgsize_max_state"
				value="selected" id="msgsize_max_state" <?cs
				if:Data.List.MsgSize.Max>0 ?>checked="checked"<?cs /if ?>>
				<label for="msgsize_max_state"><?cs var:Lang.Misc.MessageSize.Max ?></label>
				<ul><li><input type="text" name="msgsize_max_value" size="10"
				style="text-align:right" value="<?cs
				alt:Data.List.MsgSize.Max ?>30000<?cs /alt ?>"> <?cs
				var:Lang.Misc.MessageSize.Unit ?></li></ul></li>
			<li><input type="checkbox" name="msgsize_min_state"
				value="selected" id="msgsize_min_state" <?cs
				if:Data.List.MsgSize.Min>0 ?>checked="checked"<?cs /if ?>>
				<label for="msgsize_min_state"><?cs var:Lang.Misc.MessageSize.Min ?></label>
				<ul><li><input type="text" name="msgsize_min_value" size="10"
				style="text-align:right" value="<?cs
				alt:Data.List.MsgSize.Min ?>2<?cs /alt ?>"> <?cs
				var:Lang.Misc.MessageSize.Unit ?></li></ul></li>

			<!-- headerremove -->
			<li><?cs var:Lang.Misc.HeaderRemove ?>:<br/>
				<ul><li><textarea name="headerremove" rows="5" cols="70"><?cs
				var:html_escape(Data.List.HeaderRemove) ?></textarea></li></ul></li>

			<!-- headeradd -->
			<li><?cs var:Lang.Misc.HeaderAdd ?>:<br/>
				<ul><li><textarea name="headeradd" rows="5" cols="70"><?cs
				var:html_escape(Data.List.HeaderAdd) ?></textarea></li></ul></li>

			<!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

			<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>

		</ul>
	</form>
</fieldset>

<?cs include:TemplateDir + '/help_tag_susbtitution.cs' ?>
