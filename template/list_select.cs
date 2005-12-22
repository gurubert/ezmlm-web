<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ListSelect) ?></h1>
</div>

<fieldset>
	<legend>
		<?cs var:html_escape(Lang.Legend.AvailableLists) ?>
	</legend>

<!-- to get a multiple-columns-design, we do strange things ... -->
<?cs set:listnum=subcount(Data.Lists) ?>

<?cs if:listnum > 0 ?>

	<?cs if:listnum < 20 ?><?cs set:columns=1 ?><?cs
		elif:listnum < 40 ?><?cs set:columns=2 ?><?cs
		else ?><?cs set:columns=3 ?><?cs /if ?>
	<?cs set:col_len=listnum / columns ?>
	<?cs if:listnum % columns > 0 ?><?cs set:col_len = col_len + #1 ?><?cs /if ?>

	<table class="list_select">
	<?cs loop: x = #0, col_len-1, #1 ?>
	<tr>
		<?cs loop: y = #0, columns-1, #1 ?>
		<td>
			<?cs set:listname = Data.Lists[y * col_len + x] ?><?cs
				if:listname ?><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(listname) ?>&amp;action=subscribers" title="<?cs var:html_escape(listname) ?>"><?cs call:limit_string_len(html_escape(listname),18) ?></a>
				<?cs /if ?>
		</td>
		<?cs /loop ?>
	</tr>
	<?cs /loop ?>
	</table>
<?cs else ?>
	<p><?cs var:html_escape(Lang.Misc.NoListsAvailable) ?></p>
<?cs /if ?>

</fieldset>

