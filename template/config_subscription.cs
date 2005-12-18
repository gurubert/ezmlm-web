<div id="config" class="container">

    <div class="title">
	<h2><?cs var:Lang.Title.ConfigSub ?></h2>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />
    <input type="hidden" name="config_subset" value="subscription" />
    <div class="info">
	<p><?cs var:Lang.Misc.ListName ?>: <em><?cs var:Data.List.Name ?></em></p>
	<p><?cs var:Lang.Misc.ListAddress ?>: <em><?cs var:Data.List.Address ?></em></p>
    </div>

    <div class="input"><ul>

		<li><?cs call:checkbox("p") ?></li>
		<li><?cs call:checkbox("h") ?></li>
		<li><?cs call:checkbox("j") ?></li>
		<li><?cs call:checkbox("s") ?></li>

	<!-- "available_options" is filled by the checkbox macro -->
	<input type="hidden" name="options_available" value="<?cs var:available_options ?>" />

	<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
    </ul></div>

  </form>

</div>
