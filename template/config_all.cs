<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ConfigAll) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ConfigAll) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.ConfigAll) ?> </legend>

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="config_subset" value="all" />

		<ul>

			<!-- public subsccription and archive -->
			<li><?cs call:checkbox("p") ?></li>

			<!-- do not require confirmation for subscription -->
			<li><?cs call:checkbox("h") ?></li>

			<!-- do not require confirmation for unsubscribe -->
			<li><?cs call:checkbox("j") ?></li>

			<!-- moderate subscription -->
			<li><?cs call:checkbox("s") ?></li>

			<!-- use deny list -->
			<li><?cs call:checkbox("k") ?></li>

			<!-- only subscribers may post -->
			<li><?cs call:checkbox("u") ?></li>

			<!-- require confirmation from poster -->
			<li><?cs call:checkbox("y") ?></li>

			<!-- posted messages are moderated -->
			<li><?cs call:checkbox("m") ?></li>

			<!-- only moderators may post -->
			<li><?cs call:checkbox("o") ?></li>

			<!-- process mailman-style requests -->
			<li><?cs call:checkbox("q") ?></li>

			<!-- remove ezmlm-warn -->
			<li><?cs call:checkbox("w") ?></li>

			<!-- archive messages -->
			<li><?cs call:checkbox("a") ?></li>

			<!-- only moderators may access the archive -->
			<li><?cs call:checkbox("b") ?></li>

			<!-- block unknown users from archive -->
			<li><?cs call:checkbox("g") ?></li>

			<!-- remove 'no-archive' header -->
			<li><?cs call:checkbox("i") ?></li>
		
			<!-- enable remote administration -->
			<li><?cs call:checkbox("r") ?></li>

			<!-- administrators may request subscribers list -->
			<li><?cs call:checkbox("l") ?></li>

			<!-- administrators may edit text files via mail -->
			<li><?cs call:checkbox("n") ?></li>

			<!-- from address -->
			<li><?cs call:setting("3") ?></li>

			<!-- list owner address -->
			<li><?cs call:setting("5") ?></li>

			<!-- mysql database -->
			<?cs if:Data.Modules.mySQL ?>
				<li><?cs call:setting("6") ?></li><?cs /if ?>

			<!-- set main list name -->
			<li><?cs call:setting("0") ?></li>

			<!-- messsage moderator -->
			<li><?cs call:setting("7") ?></li>

			<!-- custom path to subscription moderators -->
			<li><?cs call:setting("8") ?></li>

			<!-- subject prefix -->
			<li><?cs call:checkbox("f") ?>
				<ul><li><input type="text" name="prefix" value="<?cs
					var:html_escape(Data.List.Prefix) ?>" size="70" />
				</li></ul></li>

			<!-- trailing text -->
			<li><?cs call:checkbox("t") ?>
				<?cs if:(Data.List.Options.t == 1) ?>
				<!-- turn off trailaer, if "-t" is not activated, as it will be
					removed during the next config_update -->
					<ul><li><textarea name="trailing_text" rows="3" cols="72"><?cs
						var:html_escape(Data.List.TrailingText) ?></textarea></li>
					</ul></li><?cs /if ?>

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
				<!-- turn off mimermove, if "-x" is not activated, as it will be
						removed during the next config_update -->
					<li><?cs var:html_escape(Lang.Misc.MimeReject) ?>:<br/>
						<textarea name="mimereject" rows="4" cols="70"><?cs
						var:html_escape(Data.List.MimeReject) ?></textarea></li>
					<li><?cs var:html_escape(Lang.Misc.MimeRemove) ?>:<br/>
						<textarea name="mimeremove" rows="4" cols="70"><?cs
						var:html_escape(Data.List.MimeRemove) ?></textarea></li>
				</ul><?cs /if ?></li>

			<!-- headerremove -->
			<li><?cs var:html_escape(Lang.Misc.HeaderRemove) ?>:<br/>
				<ul><li><textarea name="headerremove" rows="5" cols="70"><?cs
				var:html_escape(Data.List.HeaderRemove) ?></textarea></li></ul></li>

			<!-- headeradd -->
			<li><?cs var:html_escape(Lang.Misc.HeaderAdd) ?>:<br/>
				<ul><li><textarea name="headeradd" rows="5" cols="70"><?cs
				var:html_escape(Data.List.HeaderAdd) ?></textarea></li></ul></li>

			<!-- language -->
			<?cs if:subcount(Data.List.AvailableLanguages) > 0 ?>
				<li><label for="list_language"><?cs var:html_escape(Lang.Misc.ListLanguage)
						?>:</label>
					<select name="list_language" id="list_language">
						<?cs each:item = Data.List.AvailableLanguages ?>
							<option <?cs if:(item == Data.List.Language)
								?>selected="selected"<?cs /if ?>><?cs var:item ?></option>
						<?cs /each ?>
					</select></li><?cs /if ?>

			<!-- charset -->
			<?cs if:Data.useCharSet ?>
				<li><label for="list_charset"><?cs var:html_escape(Lang.Misc.ListCharset)
						?>:</label>
					<input type="text" name="list_charset" id="list_charset" size="30"
						value="<?cs var:Data.List.CharSet ?>" />
					</li><?cs /if ?>

			<!-- ezmlm-web administators -->
			<?cs if:Data.WebUser.show && Data.List.WebUsers ?>
				<li><?cs var:html_escape(Lang.Misc.AllowedToEdit) ?> 
					<ul><li><input type="text"
					name="webusers" value="<?cs var:html_escape(Data.List.WebUsers)
					?>" size="40" /><br/>
					</li></ul></li><?cs /if ?>

			<li><!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

			<input type="hidden" name="action" value="config_do" />
			<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button></li>
		</ul>

	</form>
</fieldset>

