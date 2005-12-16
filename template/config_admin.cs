<div id="config" class="container">

    <div class="title">
	<h2><?cs var:Lang.Title.ConfigAdmin ?></h2>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
    <div class="info">
	<p><?cs var:Lang.Misc.ListName ?>: <em><?cs var:Data.List.Name ?></em></p>
	<p><?cs var:Lang.Misc.ListAddress ?>: <em><?cs var:Data.List.Address ?></em></p>
    </div>

    <div class="input">


	<input type="checkbox" name="option_r" value="option_r" <?cs if:Data.List.Options.r ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.r ?></input>

	<input type="checkbox" name="option_l" value="option_l" <?cs if:Data.List.Options.l ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.l ?></input>
	<input type="checkbox" name="option_n" value="option_n" <?cs if:Data.List.Options.n ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.n ?></input>


	
	<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
    </div>

  </form>

</div>
