<div class="title">
	<h1><?cs var:html_escape(Lang.Title.SubscribeLog) ?></h1>
</div>

<fieldset>
	<legend><?cs var:html_escape(Lang.Legend.SubscribeLog) ?> </legend>

	<?cs if:subcount(Data.List.SubscribeLog) > 0 ?>
		<table>
		<?cs each:x = Data.List.SubscribeLog ?>
			<tr>
				<td><?cs var:html_escape(x.address) ?></td>
				<td><?cs var:html_escape(x.text) ?></td>
				<td><?cs var:html_escape(x.date) ?></td>
			</tr>
		<?cs /each ?>
		</table>
	<?cs else ?>
		<?cs var:html_escape(Lang.WarningMessage.EmptyList) ?>
	<?cs /if ?>
</fieldset>

