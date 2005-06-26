<div id="create" class="container">

    <div class="title">
	<h2><?cs var:Lang.Misc.CreateNew ?></h2>
	<hr>
    </div>


  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="state" value="create">
    <div class="input">
	<span class="formfield"><?cs var:Lang.Misc.ListName ?>: <input type="text" name="list" size="20"><?cs call:help_icon("ListName") ?></span>
	<span class="formfield"><?cs var:Lang.Misc.ListAddress ?>: <input type="text" name="inlocal" size="10" value="<?cs var:Data.UserName ?>">
	  <?cs call:help_icon("ListName") ?> @ <input type="text" name="inhost" value="<?cs var:Data.HostName ?>" size="30"><?cs call:help_icon("ListAdd") ?></span>
	<span class="formfield"><?cs var:Lang.Misc.ListOptions ?>:</span>

	<?cs include:TemplateDir + "display_options.cs" ?>

	<?cs if:Data.Modules.mySQL ?>
	<!-- Allow creation of mysql table if the module allows it -->
		<span class="formfield"><input type="checkbox" name="sql"label="<?cs var:Lang.Misc.mysqlCreate ?>" on="1"><?cs call:help_icon("mysqlCreate") ?></span>
	<?cs /if ?>

	<?cs if:Data.WebUser.show ?>
		<span class="formfield"><?cs var:Lang.Misc.AllowedToEdit ?>: <input type="text"
		  name="webusers" size="30" value="<?cs var:Data.WebUser.UserName ?>">
		  <?cs call:help_icon("WebUsers") ?></span>
		# TODO: the following span is quite unusual
		<span class="help"><?cs var:Lang.Helper.AllowEdit ?></span>
	<?cs /if ?>
    </div>

    <div class="question">
	<span class="button"><input type="submit" name="action"
	  value="<?cs var:Lang.Buttons.Create ?>"></span>
	<span class="button"><input type="reset" name="action"
	  value="<?cs var:Lang.Buttons.ResetForm ?>"></span>
	<span class="button"><input type="submit" name="action"
	  value="<?cs var:Lang.Buttons.Cancel ?>"></span>
    </div>
  </form>

</div>
