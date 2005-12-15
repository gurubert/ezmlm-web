<div id="config" class="container">

    <div class="title">
	<h2><?cs var:Lang.Misc.EditConfiguration ?></h2>
	<hr/>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
    <div class="info">
	<p><?cs var:Lang.Misc.ListName ?>: <em><?cs var:Data.List.Name ?></em></p>
	<p><?cs var:Lang.Misc.ListAddress ?>: <em><?cs var:Data.List.Address ?></em></p>
    </div>

    <div class="input">
	<h2><?cs var:Lang.Misc.List.Options ?> :</h2>

	<?cs include:TemplateDir + "display_options.cs" ?>

	<?cs if:Data.List.Prefix ?>
	  <div class="formfield"><?cs var:Lang.Misc.Prefix ?>: <input type="text" name="prefix"
	    value="<?cs var:Data.List.Prefix ?>" <?cs call:help_title("Prefix") ?> size="12"><?cs call:help_icon("Prefix") ?></div>
	<?cs /if ?>
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

    <div class="question">
	<button type="submit" name="action" value="config_main_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
	<button type="reset" name="action" value="reset"><?cs var:Lang.Buttons.ResetForm ?></button>
	<button type="submit" name="action" value="list_textfiles"><?cs var:Lang.Buttons.EditTexts ?></button>
    </div>

  </form>

</div>
