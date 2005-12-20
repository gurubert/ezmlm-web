<div id="config" class="container">

    <div class="title">
		<h1><?cs var:Lang.Title.ConfigFilter ?></h1>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="config_subset" value="filter" />

    <div class="input"><ul>

		<li><?cs call:checkbox("f") ?>
			<ul><li><div class="formfield"><?cs var:Lang.Misc.Prefix ?>: <br />
			<input type="text"
			name="prefix" value="<?cs var:Data.List.Prefix ?>" <?cs
			call:help_title("Prefix") ?> size="70" /></div>
			</li></ul></li>
		<li><?cs call:checkbox("t") ?></li>
		<li><?cs call:setting("3") ?></li>

		<li><?cs call:checkbox("x") ?>
		<?cs if:(Data.List.Options.x == 1) ?><ul>
		<!-- turn off mimermove, if "-x" is not activated, as it will be
				removed during the next config_update -->
			<li class="formfield"><?cs var:Lang.Misc.MimeRemove ?>:<br/>
				<textarea name="mimeremove" rows="5"
				cols="70"><?cs var:html_escape(Data.List.MimeRemove) ?></textarea></li>
		</ul></li><?cs /if ?>

		<li class="formfield"><input type="checkbox" name="msgsize_max_state"
			value="selected" <?cs if:Data.List.MsgSize.Max>0 ?>checked="checked"<?cs
			/if ?>> <?cs var:Lang.Misc.MessageSize.Max ?>
			<ul><li><input type="text" name="msgsize_max_value" size="10"
			style="text-align:right"
			value="<?cs alt:Data.List.MsgSize.Max ?>30000<?cs /alt ?>"> <?cs
			var:Lang.Misc.MessageSize.Unit ?></li></ul></li>
		<li class="formfield"><input type="checkbox" name="msgsize_min_state"
			value="selected" <?cs if:Data.List.MsgSize.Min>0 ?>checked="checked"<?cs
			/if ?>> <?cs var:Lang.Misc.MessageSize.Min ?>
			<ul><li><input type="text" name="msgsize_min_value" size="10"
			style="text-align:right"
			value="<?cs alt:Data.List.MsgSize.Min ?>2<?cs /alt ?>"> <?cs
			var:Lang.Misc.MessageSize.Unit ?></li></ul></li>

		<li class="formfield"><?cs var:Lang.Misc.HeaderRemove ?>:<br/>
			<ul><li><textarea name="headerremove" rows="5" cols="70"><?cs
			var:html_escape(Data.List.HeaderRemove) ?></textarea></li></ul></li>
		<li class="formfield"><?cs var:Lang.Misc.HeaderAdd ?>:<br/>
			<ul><li><textarea name="headeradd" rows="5" cols="70"><?cs
			var:html_escape(Data.List.HeaderAdd) ?></textarea></li></ul></li>

		<!-- include default form values -->
		<?cs include:TemplateDir + '/form_common.cs' ?>

		<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
    </div>

  </form>

</div>
