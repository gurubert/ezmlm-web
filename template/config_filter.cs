<div id="config" class="container">

    <div class="title">
		<h1><?cs var:Lang.Title.ConfigFilter ?></h1>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />
    <input type="hidden" name="config_subset" value="filter" />

    <div class="input"><ul>

		<li><?cs call:checkbox("f") ?>
			<ul><li><div class="formfield"><?cs var:Lang.Misc.Prefix ?>: <br />
			<input type="text"
			name="prefix" value="<?cs var:Data.List.Prefix ?>" <?cs
			call:help_title("Prefix") ?> size="70" /></div>
			</li></ul></li>

		<li><?cs call:checkbox("t") ?></li>

		<li><?cs call:checkbox("x") ?>
		<ul>
			<li><div class="formfield"><?cs var:Lang.Misc.HeaderRemove ?>:<?cs
				call:help_icon("HeaderRemove") ?>
				<textarea name="headerremove" 
				rows="5" cols="70"><?cs var:html_escape(Data.List.HeaderRemove) ?></textarea>
				</div></li>
			<li><div class="formfield"><?cs var:Lang.Misc.HeaderAdd ?>:
				<textarea name="headeradd" rows="5"
				cols="70"><?cs var:html_escape(Data.List.HeaderAdd) ?></textarea></div></li>
			<li><div class="formfield"><?cs var:Lang.Misc.MimeRemove ?>:<?cs
				call:help_icon("MimeRemove") ?><textarea name="mimeremove" rows="5"
				cols="70"><?cs var:html_escape(Data.List.MimeRemove) ?></textarea></div></li>
		</ul></li>

		<!-- TODO: Message size -->
		<li>Hier wird bald die Nachrichtengroesse limitiert</li>

		<!-- "available_options" is filled by the checkbox macro -->
		<input type="hidden" name="options_available" value="<?cs var:available_options ?>" />

		<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
    </div>

  </form>

</div>
