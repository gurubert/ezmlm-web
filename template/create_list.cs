<div id="create" class="container">

    <div class="title">
	<h2><?cs var:Lang.Misc.CreateNew ?></h2>
	<hr>
    </div>


  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <div class="input">
	<span class="formfield"><?cs var:Lang.Misc.ListName ?>: <input type="text" name="list"
		<?cs call:help_title("ListName") ?> size="20"><?cs call:help_icon("ListName") ?></span>
	<span class="formfield"><?cs var:Lang.Misc.ListAddress ?>: <input type="text" name="inlocal"
		size="10" <?cs call:help_title("ListAddress") ?> value="<?cs var:Data.UserName ?>">
		<?cs call:help_icon("ListAddress") ?> @ <input type="text" name="inhost" size="30"
	  	value="<?cs var:Data.HostName ?>" <?cs call:help_title("ListAddress") ?>><?cs call:help_icon("ListAddress") ?></span>
	<span class="formfield"><?cs var:Lang.Misc.ListOptions ?>:</span>

	<?cs include:TemplateDir + "display_options.cs" ?>

	<?cs if:Data.Modules.mySQL ?>
	<!-- Allow creation of mysql table if the module allows it -->
		<span class="formfield"><input type="checkbox" name="sql" on="1"
		label="<?cs var:Lang.Misc.mysqlCreate ?>" <?cs call:help_title("mysqlCreate") ?>><?cs call:help_icon("mysqlCreate") ?></span>
	<?cs /if ?>

	<?cs if:Data.WebUser.show ?>
		<span class="formfield"><?cs var:Lang.Misc.AllowedToEdit ?>: <input type="text"
		  name="webusers" size="30" value="<?cs var:Data.WebUser.UserName ?>"
		  <?cs call:help_title("WebUsers") ?>><?cs call:help_icon("WebUsers") ?></span>
		# TODO: the following span is quite unusual
		<span class="help"><?cs var:Lang.Helper.AllowEdit ?></span>
	<?cs /if ?>
    </div>

    <div class="question">
	<button type="submit" name="action" value="list_create_do"><?cs var:Lang.Buttons.Create ?></button>
	<button type="reset" name="action" value="reset"><?cs var:Lang.Buttons.ResetForm ?></button>
    </div>
  </form>

</div>
