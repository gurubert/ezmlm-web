<div id="delete" class="container">

    <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	<input type="hidden" name="state" value="confirm_delete">
	<input type="hidden" name="list" value="<?cs var:Data.ListName ?>">
	<div class="title">
	    <h2><?cs var:Lang.Misc.ConfirmDelete ?> <i><?cs var:Data.ListName ?></i></h2>
	    <div class="question">
		<span class="button"><input type="submit" name="confirm"
			value="<?cs var:Lang.Buttons.Yes ?>" tabindex="1"></span>
		<span class="button"><input type="submit" name="confirm"
			value="<?cs var:Lang.Buttons.No ?>" tabindex="2"></span>
	    </div>
	</div>
    </form>

</div>
