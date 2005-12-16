<div id="config" class="container">

    <div class="title">
	<h2><?cs var:Lang.Title.ConfigArchive ?></h2>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
    <div class="info">
	<p><?cs var:Lang.Misc.ListName ?>: <em><?cs var:Data.List.Name ?></em></p>
	<p><?cs var:Lang.Misc.ListAddress ?>: <em><?cs var:Data.List.Address ?></em></p>
    </div>

    <div class="input">


	<input type="checkbox" name="option_a" value="option_a" <?cs if:Data.List.Options.a ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.a ?></input>
	<input type="checkbox" name="option_b" value="option_b" <?cs if:Data.List.Options.b ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.b ?></input>
	<input type="checkbox" name="option_g" value="option_g" <?cs if:Data.List.Options.g ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.g ?></input>

	<input type="checkbox" name="option_i" value="option_i" <?cs if:Data.List.Options.i ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.i ?></input>

	<button type="submit" name="action" value="config_main_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
	</div>

  </form>

</div>
