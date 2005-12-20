<div id="create" class="container">

    <div class="title">
		<h1><?cs var:Lang.Title.ListCreate ?></h1>
    </div>


  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <div class="input"><ul>
		<li class="formfield"><?cs var:Lang.Misc.ListName ?>: <input type="text" name="list"
		<?cs call:help_title("ListName") ?> size="25"></li>
		
		<li class="formfield"><?cs var:Lang.Misc.ListAddress ?>: <input type="text"
			name="inlocal" size="20" <?cs call:help_title("ListAddress") ?>
			value="<?cs var:Data.UserName ?>"> @ <input type="text" name="inhost"
			size="30" value="<?cs var:Data.HostName ?>"
			<?cs call:help_title("ListAddress") ?>></li>
		<li><?cs var:Lang.Misc.ListOptions ?>:
		<ul>

			<li><?cs call:checkbox("p") ?></li>
			<li><?cs call:checkbox("a") ?></li>
			<li><?cs call:checkbox("u") ?></li>
			<li><?cs call:checkbox("d") ?></li>

			<?cs if:Data.Modules.mySQL ?>
			<!-- Allow creation of mysql table if the module allows it -->
				<li class="formfield"><input type="checkbox" name="sql" on="1"
				label="<?cs var:Lang.Misc.mysqlCreate ?>"
				<?cs call:help_title("MysqlCreate") ?>> ?></li>
			<?cs /if ?>
		</ul>

		<?cs if:Data.WebUser.show ?>
			<li class="formfield"><?cs var:Lang.Misc.AllowedToEdit ?>: <input type="text"
			  name="webusers" size="30" value="<?cs var:Data.WebUser.UserName ?>"
			  <?cs call:help_title("WebUsers") ?>></li>
		<?cs /if ?>

	</ul></div>

	<button type="submit" name="action" value="list_create_do"><?cs var:Lang.Buttons.Create ?></button>
  </form>

</div>
