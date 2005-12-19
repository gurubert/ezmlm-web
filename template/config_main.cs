<div id="config" class="container">

    <div class="title">
		<h1><?cs var:Lang.Title.ConfigMain ?></h1>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />
    <input type="hidden" name="config_subset" value="main" />

    <div class="input"><ul>

		<li><?cs call:checkbox("p") ?></li>
		<li><?cs call:checkbox("q") ?></li>
		<li><?cs call:checkbox("w") ?></li>

		<?cs if:Data.List.WebUsers ?><li>
			<span class="formfield">
					<?cs var:Lang.Misc.AllowedToEdit ?>: <input type="text"
					name="webusers" value="<?cs var:Data.List.WebUsers ?>"
					<?cs call:help_title("WebUsers") ?> size="30">
					<cs call:help_icon("WebUsers") ?></span>
				<span class="help"><?cs var:Lang.Helper.AllowEdit ?></span>
			</li><?cs /if ?>

	<!-- "available_options" is filled by the checkbox macro -->
	<input type="hidden" name="options_available" value="<?cs var:available_options ?>" />

	<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
    </ul></div>

  </form>

</div>
