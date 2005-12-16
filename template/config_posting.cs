<div id="config" class="container">

    <div class="title">
	<h2><?cs var:Lang.Title.ConfigPosting ?></h2>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
    <div class="info">
	<p><?cs var:Lang.Misc.ListName ?>: <em><?cs var:Data.List.Name ?></em></p>
	<p><?cs var:Lang.Misc.ListAddress ?>: <em><?cs var:Data.List.Address ?></em></p>
    </div>

    <div class="input">

	<input type="checkbox" name="option_u" value="option_u" <?cs if:Data.List.Options.u ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.u ?></input>
	<input type="checkbox" name="option_m" value="option_m" <?cs if:Data.List.Options.m ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.m ?></input>
	<input type="checkbox" name="option_o" value="option_o" <?cs if:Data.List.Options.o ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.o ?></input>
	<input type="checkbox" name="option_k" value="option_k" <?cs if:Data.List.Options.k ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.k ?></input>


	<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
    </div>

  </form>

</div>
