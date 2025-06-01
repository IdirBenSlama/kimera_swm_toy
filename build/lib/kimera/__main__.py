"""
Kimera CLI interface for lattice management and debugging
"""
import argparse
import sys
import time
from .storage import get_storage, close_storage
from .cls import get_stored_forms, clear_stored_forms


def cmd_lattice_list(args):
    """List recent EchoForms in the lattice"""
    storage = get_storage()
    
    forms = storage.list_forms(
        limit=args.limit,
        domain=args.domain
    )
    
    if not forms:
        print("No forms found in lattice")
        return
    
    print(f"{'Anchor':<30} {'Domain':<10} {'Phase':<15} {'Intensity':<10} {'Age (h)':<8}")
    print("-" * 80)
    
    now = time.time()
    for form in forms:
        age_hours = (now - form['updated_at']) / 3600
        print(f"{form['anchor']:<30} {form['domain']:<10} {form['phase']:<15} "
              f"{form['intensity_sum']:<10.3f} {age_hours:<8.1f}")
    
    print(f"\nTotal forms: {storage.get_form_count(args.domain)}")


def cmd_lattice_show(args):
    """Show detailed information about a specific form"""
    storage = get_storage()
    
    form = storage.fetch_form(args.anchor)
    if not form:
        print(f"No form found with anchor: {args.anchor}")
        return
    
    print(f"Anchor: {form.anchor}")
    print(f"Domain: {form.domain}")
    print(f"Phase: {form.phase}")
    print(f"Intensity Sum: {form.intensity_sum():.3f}")
    print(f"Terms ({len(form.terms)}):")
    
    for i, term in enumerate(form.terms):
        print(f"  {i+1}. {term.get('symbol', 'N/A')} ({term.get('role', 'N/A')}) "
              f"intensity={term.get('intensity', 0):.3f}")
        
        # Show timestamp if present
        if 'timestamp' in term:
            age_hours = (time.time() - term['timestamp']) / 3600
            print(f"     timestamp: {age_hours:.1f}h ago")
    
    if hasattr(form, 'topology') and form.topology:
        print(f"Topology: {form.topology}")


def cmd_lattice_prune(args):
    """Prune old forms from the lattice"""
    storage = get_storage()
    
    deleted_count = storage.prune_old_forms(args.older_than)
    print(f"Deleted {deleted_count} forms older than {args.older_than} days")


def cmd_lattice_decay(args):
    """Apply time-decay to all forms"""
    storage = get_storage()
    
    print(f"Applying time-decay with τ = {args.tau} days...")
    storage.apply_time_decay(args.tau)
    print("Time-decay applied to all forms")


def cmd_lattice_clear(args):
    """Clear all forms (for testing)"""
    if not args.confirm:
        print("This will delete ALL forms in the lattice!")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            print("Aborted")
            return
    
    clear_stored_forms()
    print("All lattice forms cleared")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Kimera lattice management CLI",
        prog="python -m kimera"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Lattice subcommand
    lattice_parser = subparsers.add_parser('lattice', help='Lattice management')
    lattice_subparsers = lattice_parser.add_subparsers(dest='lattice_command')
    
    # lattice list
    list_parser = lattice_subparsers.add_parser('list', help='List recent forms')
    list_parser.add_argument('--limit', type=int, default=10, help='Max forms to show')
    list_parser.add_argument('--domain', help='Filter by domain')
    list_parser.set_defaults(func=cmd_lattice_list)
    
    # lattice show
    show_parser = lattice_subparsers.add_parser('show', help='Show form details')
    show_parser.add_argument('anchor', help='Form anchor to show')
    show_parser.set_defaults(func=cmd_lattice_show)
    
    # lattice prune
    prune_parser = lattice_subparsers.add_parser('prune', help='Prune old forms')
    prune_parser.add_argument('--older-than', type=int, default=30, 
                             help='Delete forms older than N days')
    prune_parser.set_defaults(func=cmd_lattice_prune)
    
    # lattice decay
    decay_parser = lattice_subparsers.add_parser('decay', help='Apply time-decay')
    decay_parser.add_argument('--tau', type=float, default=14.0,
                             help='Decay time constant in days')
    decay_parser.set_defaults(func=cmd_lattice_decay)
    
    # lattice clear
    clear_parser = lattice_subparsers.add_parser('clear', help='Clear all forms')
    clear_parser.add_argument('--confirm', action='store_true',
                             help='Skip confirmation prompt')
    clear_parser.set_defaults(func=cmd_lattice_clear)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'lattice' and not args.lattice_command:
        lattice_parser.print_help()
        return
    
    try:
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print("\nAborted")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        close_storage()


if __name__ == '__main__':
    main()