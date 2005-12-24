<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ListCreate) ?></h1>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.ListCreate) ?> </legend>

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
		<ul>
			<li><label for="listname"><?cs var:html_escape(Lang.Misc.ListName) ?>:</label>
				<input type="text" name="list" id="listname" size="25"></li>
			
			<li><label for="listaddress"><?cs var:html_escape(Lang.Misc.ListAddress) ?>:</label>
				<input type="text" id="listaddress" name="inlocal" size="20"
				value="<?cs var:html_escape(Data.UserName)
				?>"> @ <input type="text" name="inhost" size="30" value="<?cs
				var:html_escape(Data.HostName) ?>"></li>

			<?cs if:Data.Modules.MySQL ?>
			<!-- Allow creation of mysql table if the module allows it -->
				<li><?cs call:setting("6") ?></li><?cs /if ?>


			<?cs if:Data.WebUser.show ?>
				<li><label for="webusers"><?cs var:html_escape(Lang.Misc.AllowedToEdit) ?></label>
					<ul><li><input type="text" id="webusers"
						name="webusers" size="30" value="<?cs
						var:html_escape(Data.WebUser.UserName) ?>"></li></ul></li>
			<?cs /if ?>

		</ul>

		<!-- include default form values -->
		<?cs include:TemplateDir + '/form_common.cs' ?>

		<input type="hidden" name="action" value="list_create_do" />
		<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.Create) ?></button>
	</form>

</fieldset>
