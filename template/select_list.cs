<?cs if:(Status == "unknown action") ?>
<!-- the chosen action is not specified -->

    <div class="error">
	<h1><?cs var:Data.Action ?></h1>
	<h2><?cs var:Lang.Misc.UnknownAction ?></h2>
   </div>

<?cs else ?>
<!-- print available lists and administrative buttons -->

    <div id="main" class="container">
	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	    <input type="hidden" name="state" value="select">

	    <?cs if:(Data.ListsCount > 0) ?>
	    <!-- scrollbox for available lists -->
		<div class="list">
		    <!-- Keep selection box a resonable size - suggested by Sebastian Andersson -->
		    <?cs if:(Data.ListsCount > 25) ?>
			<?cs set:Data.ScrollSize = 25 ?>
		      <?cs else ?>
			<?cs set:Data.ScrollSize = Data.ListsCount ?>
		    <?cs /if ?>
		    <select name="list" tabindex="1" size="<?cs var:Data.ScrollSize ?>">
			<?cs each:item = Data.Lists ?>
			    <option><?cs var:item ?></option>
			<?cs /each ?>
		    </select>
		</div>
	    <?cs /if ?>

	    <!-- short description -->
	    <div class="info">
	   	<ul>
		    <?cs each:item = Lang.Misc.ListSelectDescription ?>
			<li><?cs var:item ?></li>
		    <?cs /each ?>
		</ul>
	    </div>

	    <!-- the buttons -->
	    <div class="add_remove">
		<?cs if:(Data.Permissions.Create == 1) ?>
	    	<!-- button "create" -->
		    <span class="button"><input type="submit" tabindex="2" name="action"
			value="<?cs var:Lang.Buttons.Create ?>" /></span>
		<?cs /if ?>
		<?cs if:(Data.ListsCount > 0) ?>
		<!-- buttons: "edit" and "delete" -->
		    <span class="button"><input type="submit" tabindex="3" name="action"
			value="<?cs var:Lang.Buttons.Edit ?>" /></span>
		    <span class="button"><input type="submit" tabindex="4" name="action"
			value="<?cs var:Lang.Buttons.Delete ?>" /></span>
		<?cs /if ?>
	    </div>
	</form>
    </div>

<?cs /if ?>
