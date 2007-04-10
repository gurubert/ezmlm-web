<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ListDelete) ?> &quot;<?cs var:html_escape(Data.List.Name) ?>&quot;</h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ListDelete) ?></p>
</div>

<fieldset>
	<legend><?cs var:html_escape(Lang.Legend.ListDelete) ?> </legend>

	<?cs call:form_header("delete_list_confirm") ?>
	<ul>
		<li><?cs var:html_escape(Lang.Misc.ConfirmDelete) ?></li>
		<li><input type="hidden" name="action" value="list_delete_do" />
			<button type="submit" name="send" value="do"><?cs
				var:html_escape(Lang.Buttons.ConfirmDeletion) ?></button>
			</li>
	</ul>
	</form>

</fieldset>
