<div id="config" class="container">

    <div class="title">
	<h2><?cs var:Lang.Title.ConfigMain ?></h2>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
    <div class="info">
	<p><?cs var:Lang.Misc.ListName ?>: <em><?cs var:Data.List.Name ?></em></p>
	<p><?cs var:Lang.Misc.ListAddress ?>: <em><?cs var:Data.List.Address ?></em></p>
    </div>

    <div class="input">


	<input type="checkbox" name="option_p" value="option_p" <?cs if:Data.List.Options.p ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.p ?></input>

	<input type="checkbox" name="option_f" value="option_f" <?cs if:Data.List.Options.f ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.f ?></input>
	<div class="formfield"><?cs var:Lang.Misc.Prefix ?>: <input type="text" name="prefix"
	    value="<?cs var:Data.List.Prefix ?>" <?cs call:help_title("Prefix") ?> size="12"><?cs call:help_icon("Prefix") ?></div>

	<input type="checkbox" name="option_t" value="option_t" <?cs if:Data.List.Options.t ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.t ?></input>

	<input type="checkbox" name="option_x" value="option_x" <?cs if:Data.List.Options.x ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.x ?></input>
	<div class="formfield"><?cs var:Lang.Misc.HeaderRemove ?>:<?cs call:help_icon("HeaderRemove") ?>
	  <br/><textarea name="headerremove" <?cs call:help_title("HeaderRemove") ?>
	  rows="5" cols="70"><?cs var:Data.List.HeaderRemove ?></textarea></div>
	<div class="formfield"><?cs var:Lang.Misc.HeaderAdd ?>:<?cs call:help_icon("HeaderAdd") ?>
	  <br/><textarea name="headeradd" <?cs call:help_title("HeaderAdd") ?>
	  rows="5" cols="70"><?cs var:Data.List.HeaderAdd ?></textarea></div>
	<?cs if:Data.List.MimeRemove ?>
	  <div class="formfield"><?cs var:Lang.Misc.MimeRemove ?>:<?cs call:help_icon("MimeRemove") ?>
	    <br/><textarea name="mimeremove" <?cs call:help_title("MimeRemove") ?>
	    rows="5" cols="70"><?cs var:Data.List.MimeRemove ?></textarea></div>
	<?cs /if ?>

	<input type="checkbox" name="option_q" value="option_q" <?cs if:Data.List.Options.q ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.q ?></input>
	<input type="checkbox" name="option_w" value="option_w" <?cs if:Data.List.Options.w ?>checked="checked"<?cs /if ?>><?cs var:Lang.Options.w ?></input>

	<?cs if:Data.List.WebUsers ?>
	  <div>
	    <span class="formfield"><?cs var:Lang.Misc.AllowedToEdit ?>: <input type="text"
	      name="webusers" value="<?cs var:Data.List.WebUsers ?>"
	      <?cs call:help_title("WebUsers") ?> size="30">
	      <cs call:help_icon("WebUsers") ?></span>
	    <span class="help"><?cs var:Lang.Helper.AllowEdit ?></span>
	  </div>
	<?cs /if ?>
    </div>

	<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
    </div>

  </form>

</div>
