<div id="config" class="container">

    <div class="title">
	<h2><?cs var:Lang.Title.ConfigAdmin ?></h2>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
    <input type="hidden" name="config_subset" value="admin" />
    <div class="info">
	<p><?cs var:Lang.Misc.ListName ?>: <em><?cs var:Data.List.Name ?></em></p>
	<p><?cs var:Lang.Misc.ListAddress ?>: <em><?cs var:Data.List.Address ?></em></p>
    </div>

    <div class="input"><ul>

		<li><?cs call:checkbox("r") ?></li>
		<li><?cs call:checkbox("l") ?></li>
		<li><?cs call:checkbox("n") ?></li>

	<!-- "available_options" is filled by the checkbox macro -->
	<input type="hidden" name="options_available" value="<?cs var:available_options ?>" />
	
	<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
	</ul></div>

  </form>

</div>
