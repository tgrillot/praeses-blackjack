from click import Option, UsageError

class MutExOption(Option):
    def __init__(self, *args, **kwargs):
        self.mut_ex = set(kwargs.pop('mut_ex', []))
        help = kwargs.get('help', '')
        if self.mut_ex:
            ex_str = ', '.join(self.mut_ex)
            kwargs['help'] = help + (
                ' NOTE: This argument is mutually exclusive with '
                ': [' + ex_str + '].'
            )
        super(MutExOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mut_ex.intersection(opts) and self.name in opts:
            raise UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "`{}`.".format(
                    self.name,
                    ', '.join(self.mut_ex)
                )
            )

        return super(MutExOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )