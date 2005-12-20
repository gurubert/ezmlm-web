<div id="config" class="container">

    <div class="title">
		<h1><?cs var:Lang.Title.ConfigMain ?></h1>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="config_subset" value="main" />

    <div class="input"><ul>

		<li><?cs call:checkbox("p") ?></li>
		<li><?cs call:checkbox("q") ?></li>
		<li><?cs call:checkbox("w") ?></li>
		<li><?cs call:setting("5") ?></li>
		<li><?cs call:setting("0") ?></li>
		<?cs if:Data.Modules.mySQL ?>
			<li><?cs call:setting("6") ?></li>
		<?cs /if ?>

		<?cs if:Data.List.WebUsers ?><li>
			<li class="formfield">
					<?cs var:Lang.Misc.AllowedToEdit ?>: 
					<ul><li><input type="text"
					name="webusers" value="<?cs var:Data.List.WebUsers ?>"
					<?cs call:help_title("WebUsers") ?> size="30"><br/>
					<?cs var:Lang.Helper.AllowEdit ?></li></ul>
			</li><?cs /if ?>

		<!-- include default form values -->
		<?cs include:TemplateDir + '/form_common.cs' ?>

	<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
    </ul></div>

  </form>

</div>
