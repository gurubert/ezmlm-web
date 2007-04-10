<div class="title">
	<h1><?cs var:html_escape(Lang.Title.SubscribeLog) ?></h1>
</div>

<fieldset>
	<legend><?cs var:html_escape(Lang.Legend.SubscribeLog) ?> </legend>

	<?cs if:subcount(Data.List.SubscribeLog) > 0 ?>
		<table class="subscribe_log">
			<tr>
				<th><?cs var:html_escape(Lang.Misc.MailAddress) ?></th>
				<th><?cs var:html_escape(Lang.Misc.SubscribeAction) ?></th>
				<th><?cs var:html_escape(Lang.Misc.SubscribeActionDetails) ?></th>
				<th><?cs var:html_escape(Lang.Misc.Date) ?></th>
			</tr>
		<?cs loop:x = subcount(Data.List.SubscribeLog)-1, #0, -1 ?><?cs
				# we print the lines backward ?>
			<tr>
				<td><?cs var:html_escape(Data.List.SubscribeLog[x].address) ?></td>
				<td><?cs if:Data.List.SubscribeLog[x].action == '+' ?><?cs
						var:html_escape(Lang.Misc.SubscribeActions.add) ?><?cs
					elif:Data.List.SubscribeLog[x].action == '-' ?><?cs
						var:html_escape(Lang.Misc.SubscribeActions.remove) ?><?cs
					else ?><?cs var:html_escape(Lang.Misc.SubscribeActions.unknown)
					?><?cs /if ?></td>
				<td><?cs if:Data.List.SubscribeLog[x].details == 'manual' ?><?cs
						var:html_escape(Lang.Misc.SubscribeActions.manual) ?><?cs
					elif:Data.List.SubscribeLog[x].details == 'mod' ?><?cs
						var:html_escape(Lang.Misc.SubscribeActions.mod) ?><?cs
					elif:Data.List.SubscribeLog[x].details == 'auto' ?><?cs
						var:html_escape(Lang.Misc.SubscribeActions.auto) ?><?cs
					else ?><?cs var:html_escape(Lang.Misc.SubscribeActions.unknown)
					?><?cs /if ?></td>
				<td><?cs var:html_escape(Data.List.SubscribeLog[x].date) ?></td>
			</tr>
		<?cs /loop ?>
		</table>
	<?cs else ?>
		<p><?cs var:html_escape(Lang.WarningMessage.EmptyList) ?></p>
	<?cs /if ?>
</fieldset>

