<div class="title">
	<h1><?cs var:Lang.Title.ListCreate ?></h1>
</div>

<fieldset class="form">
	<legend><?cs var:Lang.Legend.ListCreate ?></legend>

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
		<ul>
			<li><label for="listname"><?cs var:Lang.Misc.ListName ?>:</label>
				<input type="text" name="list" id="listname"
				<?cs call:help_title("ListName") ?> size="25"></li>
			
			<li><label for="listaddress"><?cs var:Lang.Misc.ListAddress ?>:</label>
				<input type="text" id="listaddress" name="inlocal" size="20" <?cs
				call:help_title("ListAddress") ?> value="<?cs var:Data.UserName
				?>"> @ <input type="text" name="inhost" size="30" value="<?cs
				var:Data.HostName ?>"<?cs call:help_title("ListAddress") ?>></li>
			<li><?cs var:Lang.Misc.ListOptions ?>:
			<ul>

				<li><?cs call:checkbox("p") ?></li>
				<li><?cs call:checkbox("a") ?></li>
				<li><?cs call:checkbox("u") ?></li>
				<li><?cs call:checkbox("d") ?></li>

				<?cs if:Data.Modules.MySQL ?>
				<!-- Allow creation of mysql table if the module allows it -->
					<li><?cs call:setting("6") ?></li><?cs /if ?>

			</ul>

			<?cs if:Data.WebUser.show ?>
				<li><label for="webusers"><?cs var:Lang.Misc.AllowedToEdit ?>:</label>
					<ul><li><input type="text" id="webusers"
						name="webusers" size="30" value="<?cs var:Data.WebUser.UserName ?>"
						<?cs call:help_title("WebUsers") ?>></li></ul></li>
			<?cs /if ?>

		</ul>

		<!-- include default form values -->
		<?cs include:TemplateDir + '/form_common.cs' ?>

		<button type="submit" name="action" value="list_create_do"><?cs var:Lang.Buttons.Create ?></button>
	</form>

</fieldset>
