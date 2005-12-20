<div id="config" class="container">

    <div class="title">
		<h1><?cs var:Lang.Title.ConfigSub ?></h1>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="config_subset" value="subscription" />

    <div class="input"><ul>

		<li><?cs call:checkbox("p") ?></li>
		<li><?cs call:checkbox("h") ?></li>
		<li><?cs call:checkbox("j") ?></li>
		<li><?cs call:checkbox("s") ?></li>
		<li><?cs call:setting("8") ?></li>

		<!-- include default form values -->
		<?cs include:TemplateDir + '/form_common.cs' ?>

	<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
    </ul></div>

  </form>

</div>
