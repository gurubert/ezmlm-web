<div id="config" class="container">

    <div class="title">
		<h1><?cs var:Lang.Title.ConfigArchive ?></h1>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
    <input type="hidden" name="config_subset" value="archive" />

    <div class="input"><ul>
	
		<li><?cs call:checkbox("a") ?></li>
		<li><?cs call:checkbox("p") ?></li>
		<li><?cs call:checkbox("b") ?></li>
		<li><?cs call:checkbox("g") ?></li>
		<li><?cs call:checkbox("i") ?></li>
	
	<!-- "available_options" is filled by the checkbox macro -->
	<input type="hidden" name="options_available" value="<?cs var:available_options ?>" />

	<button type="submit" name="action" value="config_main_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
	</ul></div>

  </form>

</div>
