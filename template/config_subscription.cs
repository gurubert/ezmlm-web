<div id="config" class="container">

    <div class="title">
	<h2><?cs var:Lang.Title.ConfigSub ?></h2>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
    <div class="info">
	<p><?cs var:Lang.Misc.ListName ?>: <em><?cs var:Data.List.Name ?></em></p>
	<p><?cs var:Lang.Misc.ListAddress ?>: <em><?cs var:Data.List.Address ?></em></p>
    </div>

    <div class="input">

	<input type="checkbox" name="option_h" value="option_h" <?cs if:Data.List.Options.h ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.h ?></input>
	<input type="checkbox" name="option_j" value="option_j" <?cs if:Data.List.Options.j ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.j ?></input>
	<input type="checkbox" name="option_s" value="option_s" <?cs if:Data.List.Options.s ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.s ?></input>


	<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
    </div>

  </form>

</div>
